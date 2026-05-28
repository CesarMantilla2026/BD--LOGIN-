import React, { useState } from 'react';

export default function Login() {
  // 1. Estados para capturar las credenciales en tiempo real
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [loading, setLoading] = useState(false);

  // 2. Función asíncrona para manejar el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensaje('');

    try {
      // Usamos localhost en local. Cuando subas a Vercel, recuerda usar import.meta.env.VITE_API_URL
      const response = await fetch('http://127.0.0.1:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ 
    username: username, 
    password: password 
  }),
});

      const data = await response.json();

      if (response.ok) {
        // Si todo sale bien, Flask devuelve {"message": "..."}
        setMensaje(`🟢 ${data.message}`);
      } else {
        // CORRECCIÓN 2: Si falla, Flask devuelve {"error": "..."}. Usamos || por si acaso
        setMensaje(`🔴 Error: ${data.error || data.message || 'Credenciales incorrectas'}`);
      }
    } catch (error) {
      setMensaje('🔴 No se pudo conectar con el servidor backend.');
    } finally {
      setLoading(false);
    }
  };

  // 3. Renderizado de la Interfaz de Usuario (Tus estilos UNFV intactos)
  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '50px auto', fontFamily: 'Arial' }}>
      <h2>Iniciar Sesión (Sistemas UNFV)</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
            required
            disabled={loading}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
            required
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading} style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: loading ? 'not-allowed' : 'pointer' }}>
          {loading ? 'Verificando...' : 'Ingresar'}
        </button>
      </form>
      {mensaje && <p style={{ marginTop: '20px', fontWeight: 'bold' }}>{mensaje}</p>}
    </div>
  );
}