import grpc
import logging
from concurrent import futures

import generated.glossary_pb2 as glossary_pb2
import generated.glossary_pb2_grpc as glossary_pb2_grpc

import database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):

	def AddTerm(self, request, context):
		logging.info(f"Received AddTerm request for term: {request.term}")
		term_dict = {'term': request.term, 'definition': request.definition}
		try:
			created_term = database.add_term(term_dict)
			return glossary_pb2.Term(term=created_term['term'], definition=created_term['definition'])
		except Exception as e:
			logging.error(f"Failed to add term {request.term}: {e}")
			context.set_code(grpc.StatusCode.ALREADY_EXISTS)
			context.set_details(f"Term with term '{request.term}' already exists.")
			return glossary_pb2.Term()

	def GetTerm(self, request, context):
		logging.info(f"Received GetTerm request for term: {request.term}")
		term = database.get_term(request.term)
		if term:
			return glossary_pb2.Term(term=term['term'], definition=term['definition'])
		else:
			context.set_code(grpc.StatusCode.NOT_FOUND)
			context.set_details(f"Term with term '{request.term}' not found.")
			return glossary_pb2.Term()

	def ListTerms(self, request, context):
		logging.info("Received ListTerms request")
		terms_from_db = database.get_all_terms()
		proto_terms = [glossary_pb2.Term(term=t['term'], definition=t['definition']) for t in terms_from_db]
		return glossary_pb2.TermList(terms=proto_terms)

	def UpdateTerm(self, request, context):
		logging.info(f"Received UpdateTerm request for term: {request.term}")
		rows_affected = database.update_term(request.term, request.new_definition)

		if rows_affected > 0:
			return glossary_pb2.Term(term=request.term, definition=request.new_definition)
		else:
			context.set_code(grpc.StatusCode.NOT_FOUND)
			context.set_details(f"Term with term '{request.term}' not found, cannot update.")
			return glossary_pb2.Term()

	def DeleteTerm(self, request, context):
		logging.info(f"Received DeleteTerm request for term: {request.term}")
		rows_affected = database.delete_term(request.term)
		if rows_affected > 0:
			return glossary_pb2.Empty()
		else:
			context.set_code(grpc.StatusCode.NOT_FOUND)
			context.set_details(f"Term with term '{request.term}' not found, cannot delete.")
			return glossary_pb2.Empty()


def serve():
	database.init_db()
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServicer(), server)
	port = '50051'
	server.add_insecure_port(f'[::]:{port}')
	server.start()
	logging.info(f"Server started, listening on port {port}")
	try:
		server.wait_for_termination()
	except KeyboardInterrupt:
		logging.info("Server is shutting down.")
		server.stop(0)


if __name__ == '__main__':
	serve()
