import json
import os
import bcrypt

ARQUIVO_USUARIOS = "users.json"
ARQUIVO_CURSOS = "cursos.json"

def loadUsers():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def saveUsers(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def loadCursos():
    if os.path.exists(ARQUIVO_CURSOS):
        with open(ARQUIVO_CURSOS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def saveCursos(cursos):
    with open(ARQUIVO_CURSOS, "w", encoding="utf-8") as f:
        json.dump(cursos, f, indent=4, ensure_ascii=False)

def login(usuarios):
    print("\nLogin")
    email = input("Email: ").strip().lower()
    senha = input("Senha: ").strip().encode('utf-8')
    if email in usuarios:
        senha_hash = usuarios[email]["senha"].encode('utf-8')
        if bcrypt.checkpw(senha, senha_hash):
            nome = usuarios[email]["nome"]
            tipo = usuarios[email]["tipo"]
            print(f"Login bem-sucedido! Bem-vindo, {nome} ({tipo})")
            return email
    print("Email ou senha incorretos.")
    return None

def cadAluno(usuarios):
    print("\nCadastro de Aluno")
    email = input("Email: ").strip().lower()
    if email in usuarios:
        print("Email já cadastrado. Tente outro.")
        return
    nome = input("Nome de usuário: ").strip()
    if nome.lower().startswith("adm") or email.startswith("adm"):
        print("Esse nome/email é reservado.")
        return
    telefone = input("Telefone: ").strip()
    idade = input("Idade: ").strip()
    senha = input("Senha: ").strip().encode('utf-8')
    senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')
    usuarios[email] = {
        "nome": nome,
        "telefone": telefone,
        "idade": idade,
        "senha": senha_hash,
        "tipo": "aluno"
    }
    saveUsers(usuarios)
    print(f"Aluno {nome} cadastrado com sucesso!")

def cadProf(usuarios):
    print("\nCadastro de Professor")
    email = input("Email: ").strip().lower()
    if email in usuarios:
        print("Email já cadastrado. Tente outro.")
        return
    nome = input("Nome de usuário: ").strip()
    if nome.lower().startswith("adm") or email.startswith("adm"):
        print("Esse nome/email é reservado.")
        return
    telefone = input("Telefone: ").strip()
    idade = input("Idade: ").strip()
    senha = input("Senha: ").strip().encode('utf-8')
    senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')
    usuarios[email] = {
        "nome": nome,
        "telefone": telefone,
        "idade": idade,
        "senha": senha_hash,
        "tipo": "professor"
    }
    saveUsers(usuarios)
    print(f"Professor {nome} cadastrado com sucesso!")

def delUsers(usuarios, email):
    print("\nDeletar Conta")
    confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ").strip().lower()
    if confirmacao == "s":
        del usuarios[email]
        saveUsers(usuarios)
        print("Conta deletada com sucesso.")
        return True
    else:
        print("Operação cancelada.")
        return False

def delContas(usuarios):
    print("\nExcluir Conta de Usuário")
    email = input("Digite o email do usuário a ser excluído: ").strip().lower()
    if email in usuarios:
        if email == "adm":
            print("A conta do administrador não pode ser excluída.")
            return
        nome = usuarios[email]["nome"]
        confirmacao = input(f"Tem certeza que deseja excluir o usuário '{nome}'? (s/n): ").strip().lower()
        if confirmacao == "s":
            del usuarios[email]
            saveUsers(usuarios)
            print(f"Usuário '{nome}' excluído com sucesso.")
        else:
            print("Operação cancelada.")
    else:
        print("Usuário não encontrado.")

def listUsers(usuarios):
    for email, dados in usuarios.items():
        print(f"Nome: {dados['nome']}, Email: {email}, Tipo: {dados['tipo']}")

def listAlunos(usuarios):
    tem_alunos = False
    for email, dados in usuarios.items():
        if dados["tipo"] == "aluno":
            print(f"Aluno: {dados['nome']}, Email: {email}")
            tem_alunos = True
    if not tem_alunos:
        print("Nenhum aluno cadastrado.")

def cadCursos(cursos):
    print("\nCadastrar Curso")
    nome = input("Nome do curso: ").strip()
    descricao = input("Descrição: ").strip()
    duracao = input("Duração (em horas): ").strip()
    conteudo = input("Conteúdo do curso (texto): ").strip()
    cursos[nome] = {
        "descricao": descricao,
        "duracao": duracao,
        "conteudo": conteudo
    }
    saveCursos(cursos)
    print(f"Curso '{nome}' cadastrado com sucesso.")

def listarESelecionarCurso(cursos):
    if not cursos:
        print("Nenhum curso cadastrado.")
        return
    nomes = list(cursos.keys())

    while True:
        print("\nCursos disponíveis:")
        for i, nome in enumerate(nomes, 1):
            print(f"{i} - {nome} ({cursos[nome]['descricao']}, {cursos[nome]['duracao']}h)")
        print(f"{len(nomes)+1} - Voltar")

        escolha = input("Escolha um curso para acessar (número): ").strip()
        if not escolha.isdigit():
            print("Digite um número válido.")
            continue
        escolha = int(escolha)
        if escolha == len(nomes) + 1:
            break
        if 1 <= escolha <= len(nomes):
            curso = cursos[nomes[escolha - 1]]
            print(f"\nCurso: {nomes[escolha - 1]}")
            print(f"Descrição: {curso['descricao']}")
            print(f"Duração: {curso['duracao']} horas")
            print("\nConteúdo do Curso:\n")
            print(curso.get("conteudo", "Conteúdo não disponível."))
            input("\nPressione Enter para voltar à lista de cursos...")
        else:
            print("Opção inválida, tente novamente.")

def menu_adm(usuarios, cursos, email):
    while True:
        print("\nOlá Adm")
        print("1 - Cadastrar Professor")
        print("2 - Ver Usuários")
        print("3 - Cursos")
        print("4 - Excluir Conta de Usuário")
        print("5 - Logout")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadProf(usuarios)
        elif opcao == "2":
            listUsers(usuarios)
        elif opcao == "3":
            listarESelecionarCurso(cursos)
        elif opcao == "4":
            delContas(usuarios)
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def menu_professor(usuarios, cursos, email):
    while True:
        nome = usuarios[email]["nome"]
        print(f"\nOlá Prof. {nome}")
        print("1 - Ver Alunos")
        print("2 - Cadastrar Curso")
        print("3 - Cursos")
        print("4 - Deletar Minha Conta")
        print("5 - Logout")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            listAlunos(usuarios)
        elif opcao == "2":
            cadCursos(cursos)
        elif opcao == "3":
            listarESelecionarCurso(cursos)
        elif opcao == "4":
            if delUsers(usuarios, email):
                break
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def menu_aluno(usuarios, cursos, email):
    while True:
        dados = usuarios[email]
        print(f"\nOlá {dados['nome']}")
        print("1 - Ver Meus Dados")
        print("2 - Cursos")
        print("3 - Deletar Minha Conta")
        print("4 - Logout")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            print(f"Nome: {dados['nome']}")
            print(f"Email: {email}")
            print(f"Telefone: {dados['telefone']}")
            print(f"Idade: {dados['idade']}")
        elif opcao == "2":
            listarESelecionarCurso(cursos)
        elif opcao == "3":
            if delUsers(usuarios, email):
                break
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

def inicio():
    print("Bem-vindo à plataforma Vai de Curso")
    usuarios = loadUsers()
    cursos = loadCursos()

    while True:
        print("\nTela Inicial")
        print("1 - Login")
        print("2 - Cadastro Aluno")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            email_logado = login(usuarios)
            if email_logado:
                tipo_usuario = usuarios[email_logado]["tipo"]
                if tipo_usuario == "adm":
                    menu_adm(usuarios, cursos, email_logado)
                elif tipo_usuario == "professor":
                    menu_professor(usuarios, cursos, email_logado)
                else:
                    menu_aluno(usuarios, cursos, email_logado)
        elif opcao == "2":
            cadAluno(usuarios)
        elif opcao == "3":
            print("Obrigado por usar o Vai de Curso! Até a próxima.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    inicio()
