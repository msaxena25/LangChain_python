
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    StrictInt,
    SecretStr,
    HttpUrl,
    EmailStr,
    StringConstraints,
    field_validator,
    model_validator,
    computed_field,
)


# =====================================================
# 1. ENUMS AND LITERAL TYPES
# =====================================================

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"


# Literal restricts values to a fixed set.
ProductCategory = Literal[
    "electronics", "clothing", "books"
]


# =====================================================
# 2. NESTED MODELS
# =====================================================

class Brand(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    website: HttpUrl | None = None


class Dimensions(BaseModel):
    length: float = Field(gt=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    unit: Literal["cm", "inch"] = "cm"


class Review(BaseModel):
    username: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ProductVariant(BaseModel):
    size: str | None = None
    color: str | None = None
    sku: str
    stock: int = Field(ge=0, default=0)


# =====================================================
# 3. MAIN PRODUCT MODEL
# =====================================================

class Product(BaseModel):

    # Model-level configuration
    model_config = ConfigDict(
        extra="forbid",              # Reject unknown fields
        str_strip_whitespace=True,   # Strip string whitespace
        validate_assignment=True,    # Validate attribute updates
        populate_by_name=True,       # Allow field name or alias
        json_schema_extra={
            "examples": [
                {
                    "productId": 101,
                    "name": "Laptop",
                    "price": "75000.00",
                    "category": "electronics"
                }
            ]
        }
    )

    # Required fields
    id: int = Field(
        alias="productId",
        gt=0,
        description="Unique product identifier"
    )

    name: str = Field(
        min_length=2,
        max_length=100,
        title="Product Name"
    )

    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    category: ProductCategory

    # Enum field
    status: ProductStatus = ProductStatus.ACTIVE

    # Optional value: key may be omitted
    description: str | None = None

    # Numeric constraints
    discount_percent: float = Field(
        default=0,
        ge=0,
        le=100
    )

    stock: StrictInt = Field(default=0, ge=0)

    # String constraints and regular expressions
    sku: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=20,
            pattern=r"^[A-Za-z0-9-]+$"
        )
    ]

    # Collections
    tags: list[str] = Field(default_factory=list)

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    # Nested models
    brand: Brand
    dimensions: Dimensions | None = None

    variants: list[ProductVariant] = Field(
        default_factory=list
    )

    reviews: list[Review] = Field(
        default_factory=list
    )

    # Special types
    support_email: EmailStr | None = None

    supplier_url: HttpUrl | None = None

    api_secret: SecretStr | None = None

    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # Field validator: validate or transform one field
    @field_validator("sku")
    @classmethod
    def normalize_sku(cls, value: str) -> str:
        return value.upper()

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        return value

    # Model validator: validate multiple fields together
    @model_validator(mode="after")
    def validate_product(self):
        if (
            self.status == ProductStatus.OUT_OF_STOCK
            and self.stock > 0
        ):
            raise ValueError(
                "Out-of-stock product cannot have stock"
            )
        return self

    # Computed field: derived from other fields
    @computed_field
    @property
    def final_price(self) -> Decimal:
        discount = Decimal(str(self.discount_percent))
        return (
            self.price * (Decimal("100") - discount)
            / Decimal("100")
        ).quantize(Decimal("0.01"))


# =====================================================
# 4. CREATE A PRODUCT WITH NESTED DATA
# =====================================================

product_data = {
    "productId": 101,
    "name": " Laptop ",
    "price": "75000.00",
    "category": "electronics",
    "status": "active",
    "discount_percent": 10,
    "stock": 25,
    "sku": "lap-101",
    "tags": ["computer", "work"],
    "attributes": {
        "processor": "Intel i7",
        "ram_gb": 16
    },
    "brand": {
        "name": "Example Brand",
        "website": "https://example.com"
    },
    "dimensions": {
        "length": 35.0,
        "width": 25.0,
        "height": 2.0,
        "unit": "cm"
    },
    "variants": [
        {
            "size": "16GB RAM",
            "color": "Silver",
            "sku": "lap-101-s",
            "stock": 10
        }
    ],
    "reviews": [
        {
            "username": "Amit",
            "rating": 5,
            "comment": "Excellent product"
        }
    ],
    "support_email": "support@example.com",
    "supplier_url": "https://example.com/supplier",
    "api_secret": "my-secret-value"
}


# Validate input and create the model
product = Product.model_validate(product_data)

print(product.name)
print(product.price)
print(product.final_price)
print(product.brand.name)
print(product.variants[0].sku)

# Output:
# Laptop
# 75000.00
# 67500.00
# Example Brand
# LAP-101-S


# =====================================================
# 5. FIELD ACCESS AND VALIDATION
# =====================================================

# Pydantic converts compatible input types.
print(type(product.price))  # Decimal

# Update assignment is validated.
product.stock = 30

# Invalid updates raise ValidationError.
# product.stock = -5

# Extra fields are rejected.
# Product(..., unknown_field="value")


# =====================================================
# 6. SERIALIZATION
# =====================================================

# Python dictionary
product_dict = product.model_dump()

# Use aliases, e.g. productId instead of id
product_with_alias = product.model_dump(
    by_alias=True
)

# JSON string
product_json = product.model_dump_json(indent=2)

# Exclude optional fields whose values are None
product_without_none = product.model_dump(
    exclude_none=True
)

# Hide the secret when exporting
safe_product = product.model_dump(
    exclude={"api_secret"}
)

print(product_dict)
print(product_json)


# =====================================================
# 7. VALIDATE PYTHON DATA OR JSON
# =====================================================

# Validate a Python dictionary
validated = Product.model_validate(product_data)

# Validate JSON text
validated_from_json = Product.model_validate_json(
    product_json
)

# Generate JSON Schema
schema = Product.model_json_schema(by_alias=True)

print(schema)


# =====================================================
# 8. ERROR HANDLING
# =====================================================

from pydantic import ValidationError

try:
    Product.model_validate({
        **product_data,
        "price": -100
    })
except ValidationError as error:
    print(error)


# =====================================================
# 9. OTHER USEFUL PYDANTIC FEATURES
# =====================================================

# Strict types: StrictInt, StrictStr, StrictBool
# Optional values: str | None
# Defaults: Field(default=...)
# Dynamic defaults: Field(default_factory=...)
# Constraints: gt, ge, lt, le, min_length, max_length
# Patterns: pattern=r"..."
# Aliases: alias="productId"
# Metadata: title, description, examples
# Extra fields: extra="forbid" / "ignore" / "allow"
# Validators: field_validator, model_validator
# Computed properties: computed_field
# Serialization: model_dump, model_dump_json
# Parsing: model_validate, model_validate_json
# Schema: model_json_schema()
