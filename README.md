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

```Bash
# .env file

JWKS_URL="https://YOUR_AUTH0_DOMAIN/.well-known/jwks.json"
AUDIENCE="YOUR_AUTH0_API_IDENTIFIER"
ISSUER="https://YOUR_AUTH0_DOMAIN/"
```

## Usage

Add dependency to the routes:

```python
# main.py

from contextlib import asynccontextmanager
from fauthy import JWTBearer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Application lifespan context manager. """
    app.auth = JWTBearer()

    app.include_router(
        firm_routes, tags=["Firms"], prefix="/firms", dependencies=[Depends(app.auth)]
    )
```

Decorate views to check permissions:

```python
#routes.py

from fauthy import get_user_claims, permissions_required

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
