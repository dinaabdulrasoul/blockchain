new_transactions = ['alica pays bob 50', 'Dina pays bob 100', 'alice receives 50']

# import sha256
from hashlib import sha256 
# sets the amount of leading zeros that must be found in the hash produced by the nonce
difficulty = 2
nonce = 0

# creating the proof 
proof =  sha256((str(nonce)+ str(new_transactions)).encode()).hexdigest()
# printing proof
print(proof)

# finding a proof that has 2 leading zeros
final_proof = proof
while final_proof[:2] != '0'*difficulty:
  nonce += 1
  print("Value of Nonce ", nonce)
  final_proof =  sha256((str(nonce)+ str(new_transactions)).encode()).hexdigest()
# printing final proof that was found
print("Final Proof of work", final_proof)

