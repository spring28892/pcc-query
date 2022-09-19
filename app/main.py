from fastapi import FastAPI
from app.internal.pcc import get_license_info

def create_app():
    # Initialize FastAPI app
    app = FastAPI()

    @app.get('/')
    def root():
        return {"message": "Hello World!"}

    @app.get('/pcc/{eng_id}')
    def get_info_by_eng_id(eng_id: str):
        if get_license_info(eng_id) is not None:
            username, prac_license_id, status, company, license_id, valid_time_start, valid_time_end, proof_time, penalty = get_license_info(eng_id)
            return {
                "username": username,
                "prac_license_id": prac_license_id,
                "status": status,
                "company": company,
                "license_id": license_id,
                "valid_time_start": valid_time_start,
                "valid_time_end": valid_time_end,
                "proof_time": proof_time,
                "penalty": penalty
            }
        else:
            return "Invalid user id"

    return app

application = create_app()