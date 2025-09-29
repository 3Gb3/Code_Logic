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
const nomeContainer = document.getElementById("nome-container");

toggleAuth.addEventListener("click", () => {
  isCadastro = !isCadastro;

  if (isCadastro) {
    formTitle.textContent = "Cadastrar no CodeLogic";
    submitBtn.textContent = "Cadastrar";
    toggleLink.textContent = "Entrar";
    toggleAuth.childNodes[0].textContent = "Já tem conta? ";
    nomeContainer.style.display = "flex";
  } else {
    formTitle.textContent = "Entrar no CodeLogic";
    submitBtn.textContent = "Entrar";
    toggleLink.textContent = "Cadastre-se";
    toggleAuth.childNodes[0].textContent = "Não tem conta? ";
    nomeContainer.style.display = "none";
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
  if (isCadastro && !nome) {
    showError("Por favor, informe seu nome.");
    return;
  }

  try {
    let userCred;
    if (isCadastro) {
      // Cria usuário
      userCred = await createUserWithEmailAndPassword(auth, email, senha);

      // Atualiza perfil com o nome
      await updateProfile(userCred.user, { displayName: nome });

      // Salva no localStorage
      localStorage.setItem("userName", nome);

      // Salva no Firestore
      await setDoc(doc(db, "usuarios", userCred.user.uid), {
        nome: nome,
        email: email,
        criadoEm: new Date()
      });
    } else {
      // Login
      userCred = await signInWithEmailAndPassword(auth, email, senha);

      // Salva nome no localStorage se existir
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