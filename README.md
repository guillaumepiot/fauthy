# Fauthy

**Fauthy** is a lightweight and secure authentication solution for FastAPI applications, specifically designed to integrate with **Auth0**. It simplifies the process of adding Auth0-based authentication and user management to your FastAPI projects.

## Features

- 🔒 **Auth0 Integration**: Seamless support for Auth0 authentication workflows.
- ⚡ **Lightweight**: Minimal dependencies to keep your app fast and efficient.
- 🔧 **Easy to Use**: Pre-configured helpers for token validation, user management, and secure routes.

## Installation

Install **Fauthy** using pip:

```bash
pip install fauthy
```

## Settings

```
# .env

export JWKS_URL="..."
export AUDIENCE="..."
export ISSUER="..."
```

## Usage

Add dependency to the routes:

```python
# main.py

from contextlib import asynccontextmanager
from app.lib.jwtbearer import JWTBearer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and close the MongoDB connection on startup and shutdown."""
    app.auth = JWTBearer()

    app.include_router(
        firm_routes, tags=["Firms"], prefix="/firms", dependencies=[Depends(app.auth)]
    )
```

Decorate views to check permissions:

```python
#routes.py

from app.lib.jwtbearer import get_user_claims
from app.lib.permissions import permissions_required

router = APIRouter()

@router.post(
    "",
    response_description="Add new",
    response_model=ModelName,
    status_code=status.HTTP_201_CREATED,
)
@permissions_required("update:modelname")
async def create(
    db_engine: AIOEngine = Depends(get_db_engine),
    data: ModelNameCreate = Body(...),
    claims: str = Depends(get_user_claims),
) -> Firm:
    """
    Create a new model name.
    """
```