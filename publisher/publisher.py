import sys
import data
import logging
from bottle import route, run, get, post, static_file, request, response

logger = logging.getLogger('publisher')
hdlr = logging.FileHandler('/tmp/publisher.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

@get('/orders/<id>')
def getOrders(id):
   if not id in data.student_ids:
      return err400("Access denied because SJSU id was invalid")
   
   version = data.student_ids[id]
   # reset to zero since it has 3 versions.
   if version == 2:
      data.student_ids[id] = 0
   else:   
      data.student_ids[id] = version + 1
   
   logger.info('::get::orders::' + id)
   return { 'shipped_books' : data.shipments[version] }
   
@post('/orders')
def receiveOrder():
   if not 'id' in request.json:
      return err400('id was missing')
      
   id = request.json['id']
   if not id in data.student_ids:
      return err400("The SJSU id was invalid")
   
   if not 'order_book_isbns' in request.json:
      return err400('order_book_isbns list was missing')
   
   isbns = request.json['order_book_isbns']
   if not type(isbns) is list:
      return err400('order_book_isbns must be an array')
      
   if len(isbns) < 1:
      return err400('order_book_isbns list must contain at least one isbn')
   else:
      logger.info('::post::orders::' + id)
      print request.json
      return { 'msg': 'Your order was successfully submitted.' }

@get('/log')
def showLog():
   return static_file('publisher.log', root='/tmp/')
         
def err400(errMsg):
   response.status = 400
   return { 'err': errMsg }
            
def main(_port):
   # let the server listen to all interfaces 
   run(host='0.0.0.0', port=_port)
   
if __name__ == "__main__":
   # Default port is 9000
   port = 9000
   if len(sys.argv) > 1:
      port = int(sys.argv[1])
   
   main(port)
