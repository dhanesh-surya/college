import random
import string

# Generate a 50-character SECRET_KEY
chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(random.choice(chars) for _ in range(50))

print("Generated SECRET_KEY:")
print(secret_key)
print("\nFor Render deployment, set this environment variable:")
print(f"SECRET_KEY={secret_key}")
