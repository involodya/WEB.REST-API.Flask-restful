from flask_restful import reqparse

job_parser = reqparse.RequestParser()
job_parser.add_argument('job', required=True)
job_parser.add_argument('team_leader', required=True, type=int)
job_parser.add_argument('work_size', required=True, type=int)
job_parser.add_argument('collaborators', required=True)
job_parser.add_argument('is_finished', required=True, type=bool)

user_parser = reqparse.RequestParser()
user_parser.add_argument('surname', required=True)
user_parser.add_argument('name', required=True)
user_parser.add_argument('age', required=True, type=int)
user_parser.add_argument('position', required=True)
user_parser.add_argument('speciality', required=True)
user_parser.add_argument('address', required=True)
user_parser.add_argument('email', required=True)
