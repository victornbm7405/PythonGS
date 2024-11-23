import pandas as pd

data = {"Nome": ["Produto A", "Produto B"], "Custo": [100, 200]}
df = pd.DataFrame(data)

df.to_excel("teste.xlsx", index=False)
print("Arquivo Excel gerado com sucesso!")
