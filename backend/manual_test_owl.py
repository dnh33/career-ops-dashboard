import asyncio
from app.services.owl_alpha import extract_company, assess_legitimacy, suggest_role_title

async def main():
    # Test 1: extract_company
    r1 = await extract_company('Google is hiring for AI roles')
    print(f"extract_company: {r1!r}")

    # Test 2: empty input
    r2 = await extract_company('')
    print(f"extract_company empty: {r2!r}")

    # Test 3: assess_legitimacy
    r3 = await assess_legitimacy('Google is a well-known tech company hiring software engineers.')
    print(f"assess_legitimacy: {r3!r}")

    # Test 4: suggest_role_title
    r4 = await suggest_role_title('Looking for a person to manage cloud infrastructure and DevOps')
    print(f"suggest_role_title: {r4!r}")

    # Test 5: empty suggest
    r5 = await suggest_role_title('')
    print(f"suggest_role_title empty: {r5!r}")

asyncio.run(main())
