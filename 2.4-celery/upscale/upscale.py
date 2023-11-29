import time
import os
import base64
import numpy
import cv2
from cv2 import dnn_superres
from flask import Flask, request, jsonify
from flask.views import MethodView
from celery import Celery
from celery.result import AsyncResult


app = Flask('app')

BROKER = os.getenv('BROKER')
BACKEND = os.getenv('BACKEND')

celery_app = Celery(broker=BROKER, backend=BACKEND)
celery_app.conf.update(app.config)

class ContextTask(celery_app.Task):

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask


@celery_app.task(name='upscale-image')
def upscale(input_path: str) -> str:
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel('EDSR_x2.pb')
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    result_to_string = cv2.imencode('.png', result)[1]
    result_decode = base64.b64encode(result_to_string).decode()
    return result_decode
    

class Upscaled(MethodView):

    def post(self):
        image_path = request.json.get('input_path')
        task = upscale.delay(image_path)
        return jsonify({"task_id": task.id})
    
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_app)
        result_to_string = task.result
        result_encode = base64.b64decode(result_to_string)
        from_buffer = numpy.frombuffer(result_encode, dtype=numpy.uint8)
        upscaled_img = cv2.imdecode(from_buffer, flags=1)
        cv2.imshow(f'{time.strftime("%H:%M:%S", time.localtime())}.png', upscaled_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return jsonify({'task_status': task.status})



app.add_url_rule('/upscale', view_func=Upscaled.as_view('photo_upscaling'), methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=Upscaled.as_view('status_returning'), methods=['GET'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
