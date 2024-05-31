from app.database import _async_main, criar_questionarios
import asyncio

if __name__ == "__main__":
    print("Dropping and re/creating tables")
    asyncio.run(_async_main())
    asyncio.run(criar_questionarios())
    print("Done.")
