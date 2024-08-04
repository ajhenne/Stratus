from werkzeug.security import generate_password_hash, check_password_hash
import os

# created by henne

hashed = generate_password_hash('')
# print(hashed)
admin_hashed_pass = os.getenv('STRATUS_KEY')
# print(admin_hashed_pass)
print(check_password_hash(hashed, ''))
print(check_password_hash(admin_hashed_pass, ''))