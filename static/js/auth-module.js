// Firebase authentication module for templates
// Este script é incluído nas páginas que precisam de autenticação Firebase

// Função para carregar o módulo Firebase
const loadFirebaseAuth = async () => {
    try {
        // Importa Firebase SDK
        const { initializeApp } = await import("https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js");
        const { getAuth } = await import("https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js");
        
        // Importa configuração Firebase
        const { firebaseConfig } = await import("../js/firebase-config.js");
        
        // Inicializa Firebase
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        
        return { app, auth };
    } catch (error) {
        console.error("Erro ao carregar Firebase:", error);
        return null;
    }
};

// Função para verificar autenticação
const checkAuth = (auth) => {
    return new Promise((resolve) => {
        auth.onAuthStateChanged((user) => {
            if (!user) {
                // Redireciona para login se não autenticado
                window.location.href = "/";
            } else {
                resolve(user);
            }
        });
    });
};

// Exporta para uso nos templates
window.loadFirebaseAuth = loadFirebaseAuth;
window.checkAuth = checkAuth;