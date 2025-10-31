import grpc
import logging

import generated.glossary_pb2 as glossary_pb2
import generated.glossary_pb2_grpc as glossary_pb2_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run():
	with grpc.insecure_channel('localhost:50051') as channel:
		stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

		print("--- 1. Adding new terms ---")
		try:
			response = stub.AddTerm(glossary_pb2.AddTermRequest(term="gRPC", definition="A high performance, open source universal RPC framework."))
			print(f"Added term 'gRPC': {response.term}")

			response = stub.AddTerm(glossary_pb2.AddTermRequest(term="Protobuf", definition="Protocol buffers, Google's language-neutral..."))
			print(f"Added term 'Protobuf': {response.term}")

			# Попробуем добавить дубликат (будет ошибка)
			stub.AddTerm(glossary_pb2.AddTermRequest(term="gRPC", definition="Duplicate attempt."))
		except grpc.RpcError as e:
			print(f"Error adding duplicate 'gRPC': {e.code()} - {e.details()}")

		print("\n--- 2. Listing all terms ---")
		try:
			response = stub.ListTerms(glossary_pb2.Empty())
			if not response.terms:
				print("Glossary is empty.")
			for term in response.terms:
				print(f"- {term.term}: {term.definition}")
		except grpc.RpcError as e:
			print(f"Error listing terms: {e.code()} - {e.details()}")

		print("\n--- 3. Getting a specific term ---")
		try:
			term = stub.GetTerm(glossary_pb2.TermRequest(term="gRPC"))
			print(f"Got term 'gRPC': {term.definition}")
		except grpc.RpcError as e:
			print(f"Error getting term 'gRPC': {e.code()} - {e.details()}")

		print("\n--- 4. Updating a term ---")
		try:
			updated_term = stub.UpdateTerm(glossary_pb2.UpdateTermRequest(term="gRPC", new_definition="gRPC is a modern RPC framework."))
			print(f"Updated term 'gRPC': {updated_term.definition}")
		except grpc.RpcError as e:
			print(f"Error updating term 'gRPC': {e.code()} - {e.details()}")

		print("\n--- 5. Getting a non-existent term ---")
		try:
			stub.GetTerm(glossary_pb2.TermRequest(term="REST"))
		except grpc.RpcError as e:
			if e.code() == grpc.StatusCode.NOT_FOUND:
				print(f"Correctly handled error for non-existent term: {e.details()}")
			else:
				print(f"An unexpected error occurred: {e}")

		print("\n--- 6. Deleting a term ---")
		try:
			stub.DeleteTerm(glossary_pb2.TermRequest(term="Protobuf"))
			print("Deleted term 'Protobuf'.")
		except grpc.RpcError as e:
			print(f"Error deleting term 'Protobuf': {e.code()} - {e.details()}")

		print("\n--- 7. Final list of terms ---")
		try:
			final_list = stub.ListTerms(glossary_pb2.Empty())
			if not final_list.terms:
				print("Glossary is now empty.")
			for term in final_list.terms:
				print(f"- {term.term}: {term.definition}")
		except grpc.RpcError as e:
			print(f"Error listing final terms: {e.code()} - {e.details()}")


if __name__ == '__main__':
	run()
