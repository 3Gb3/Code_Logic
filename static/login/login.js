// SDK Firebase via CDN
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import { 
  getAuth, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  updateProfile
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-firestore.js";
import { firebaseConfig } from "../js/firebase-config.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app); // Firestore

// Helpers de erro
const showError = (msg) => {
  const el = document.getElementById("error");
  el.textContent = msg;
  el.style.display = "block";
};
const clearError = () => {
  const el = document.getElementById("error");
  el.textContent = "";
  el.style.display = "none";
};

// Alternância login/cadastro
let isCadastro = false;
const formTitle = document.getElementById("form-title");
const submitBtn = document.getElementById("submit-btn");
const toggleAuth = document.getElementById("toggle-auth");
const toggleLink = document.getElementById("toggle-link");
const toggleText = document.getElementById("toggle-text");
const nomeContainer = document.getElementById("nome-container");

toggleLink.addEventListener("click", () => {
  isCadastro = !isCadastro;

  if (isCadastro) {
    formTitle.textContent = "Criar Conta no CodeLogic";
    submitBtn.querySelector('.btn-text').textContent = "Cadastrar";
    toggleLink.textContent = "Entre aqui";
    toggleText.textContent = "Já tem conta?";
    nomeContainer.classList.add('show');
  } else {
    formTitle.textContent = "Entrar no CodeLogic";
    submitBtn.querySelector('.btn-text').textContent = "Entrar";
    toggleLink.textContent = "Cadastre-se aqui";
    toggleText.textContent = "Não tem conta?";
    nomeContainer.classList.remove('show');
  }

  clearError();
});

// Login/Cadastro com Email/Senha
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  clearError();
  
  const nome = document.getElementById("nome")?.value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  // Validação do nome no cadastro
  if (isCadastro) {
    if (!nome) {
      showError("Por favor, informe seu nome.");
      return;
    }
    
    // Verifica se é nome completo (tem pelo menos um espaço)
    if (!nome.includes(' ') || nome.split(' ').filter(n => n.length > 0).length < 2) {
      showError("Por favor, informe seu nome completo (nome e sobrenome).");
      return;
    }
  }

  try {
    let userCred;
    if (isCadastro) {
      // Cria usuário
      userCred = await createUserWithEmailAndPassword(auth, email, senha);

      // Extrai o primeiro nome
      const primeiroNome = nome.split(' ')[0];

      // Atualiza perfil com o primeiro nome
      await updateProfile(userCred.user, { displayName: primeiroNome });

      // Salva o primeiro nome no localStorage
      localStorage.setItem("userName", primeiroNome);

      // Salva no Firestore com nome completo
      await setDoc(doc(db, "usuarios", userCred.user.uid), {
        nomeCompleto: nome,
        primeiroNome: primeiroNome,
        email: email,
        criadoEm: new Date()
      });
    } else {
      // Login
      userCred = await signInWithEmailAndPassword(auth, email, senha);

      // Salva primeiro nome no localStorage se existir
      if (userCred.user.displayName) {
        localStorage.setItem("userName", userCred.user.displayName);
      }
    }

    const token = await userCred.user.getIdToken();

    // Chama rota protegida
    const res = await fetch("/api/protegido", {
      headers: { Authorization: `Bearer ${token}` }
    });
    let data;
    try {
      data = await res.json();
    } catch (e) {
      showError("Erro inesperado do servidor. Tente novamente mais tarde.");
      return;
    }

    if (data.ok) {
      window.location.href = "/dashboard";
    } else if (data.error) {
      showError(data.error);
    } else {
      showError("Erro de autenticação.");
    }

  } catch (err) {
    console.error(err);
    if (isCadastro) {
      let msg = "Falha no cadastro. Verifique o email e senha.";
      if (err.code === "auth/email-already-in-use") msg = "Este email já está cadastrado.";
      else if (err.code === "auth/invalid-email") msg = "Email inválido.";
      else if (err.code === "auth/weak-password") msg = "A senha deve ter pelo menos 6 caracteres.";
      showError(msg);
    } else {
      showError("Falha no login. Verifique email e senha.");
    }
  }
});