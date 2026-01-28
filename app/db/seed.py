import asyncio
import sys
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.session import AsyncSessionLocal
from app.models.category import Category

CATEGORIES = [
    {
        "title": "Electronics",
        "slug": "electronics",
        "description": "Phones, laptops, tablets, TVs, cameras, and other electronic devices"
    },
    {
        "title": "Furniture",
        "slug": "furniture",
        "description": "Tables, chairs, sofas, beds, cabinets, and home furniture"
    },
    {
        "title": "Clothing & Accessories",
        "slug": "clothing",
        "description": "Shirts, pants, shoes, bags, jewelry, and fashion accessories"
    },
    {
        "title": "Books & Media",
        "slug": "books",
        "description": "Textbooks, novels, magazines, CDs, DVDs, and digital media"
    },
    {
        "title": "Vehicles",
        "slug": "vehicles",
        "description": "Cars, motorcycles, bicycles, scooters, and auto parts"
    },
    {
        "title": "Home & Garden",
        "slug": "home-garden",
        "description": "Tools, plants, decor, appliances, and home improvement items"
    },
    {
        "title": "Sports & Outdoors",
        "slug": "sports",
        "description": "Exercise equipment, bikes, camping gear, and sporting goods"
    },
    {
        "title": "Toys & Games",
        "slug": "toys-games",
        "description": "Board games, video games, action figures, and children's toys"
    },
    {
        "title": "Art & Collectibles",
        "slug": "art-collectibles",
        "description": "Paintings, sculptures, vintage items, and collectible memorabilia"
    },
    {
        "title": "Other",
        "slug": "other",
        "description": "Miscellaneous items that don't fit other categories"
    },
]


async def seed_categories():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Category))
            existing_categories = result.scalars().all()
            
            if existing_categories:
                return 0
            
            categories_count = 0
            for cat in CATEGORIES:
                category = Category(**cat)
                session.add(category)
                categories_count += 1
            await session.commit()

            return categories_count
        except IntegrityError as e:
            await session.rollback()
            print("this may mean that a category exist")
            return 0
        except Exception as e:
            await session.rollback()
            print("there is an error")
            print(e)
            raise

async def verify():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).order_by(Category.id))
        categories = result.scalars().all()

        if not categories:
            print("no categories found!!")
        
        for cat in categories:
            print(f"id:{cat.id}, title:{cat.title}, slug:{cat.slug}")


async def seed_all():
    try:
        created_categories = await seed_categories()

        await verify()
        print(f"we have created {created_categories} categories")
        return 0
    except Exception as e:
        print("seeding faild")
        print(e)
        return 1

def main():
    exit_code = asyncio.run(seed_all())
    sys.exit(exit_code)

if __name__ == "__main__":
    main()