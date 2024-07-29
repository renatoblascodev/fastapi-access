import random
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.service_plan import Contract, Product, ServicePlan

DATABASE_URL = 'postgresql://postgres:Yuri100100@127.0.0.1:5435/acesso'


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_fake_data():
    db = SessionLocal()
    try:
        # Create a fake contract
        contract = Contract(
            uuid=uuid.uuid4(),
            version="1.0",
            document_uri="http://example.com/contract"
        )
        db.add(contract)
        db.commit()

        # Create fake products
        products = [
            Product(
                uuid=uuid.uuid4(),
                name=f"Product {i}",
                description=f"Description for product {i}"
            ) for i in range(10)
        ]
        db.add_all(products)
        db.commit()

        # Create fake service plans
        for i in range(5):
            service_plan = ServicePlan(
                uuid=uuid.uuid4(),
                name=f"Service Plan {i}",
                trial=bool(random.getrandbits(1)),
                trial_days=random.randint(0, 30),
                contract_uuid=contract.uuid
            )
            service_plan.products = random.sample(products, k=random.randint(1, len(products)))
            db.add(service_plan)

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

if __name__ == "__main__":
    create_fake_data()
