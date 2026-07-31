const API = {
    base: '/api',

    getCsrfToken() {
        const cookies = document.cookie.split('; ');
        for (const c of cookies) {
            const [name, ...rest] = c.split('=');
            if (name === 'csrftoken') return rest.join('=');
        }
        return '';
    },

    async init() {
        const res = await fetch(`${this.base}/csrf/`, { credentials: 'include' });
        if (!res.ok) throw new Error('No se pudo obtener el token CSRF');
        return res.json();
    },

    async request(method, path, body = null) {
        const opts = {
            method,
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
        };
        if (body) opts.body = JSON.stringify(body);
        if (['POST', 'PUT', 'DELETE'].includes(method)) {
            opts.headers['X-CSRFToken'] = this.getCsrfToken();
        }
        const res = await fetch(`${this.base}${path}`, opts);
        let data;
        try {
            data = await res.json();
        } catch {
            data = { error: `Error ${res.status} - ${res.statusText}` };
        }
        if (!res.ok) throw data;
        return data;
    },

    login(email, password) {
        return this.request('POST', '/login/', { email, password });
    },
    logout() {
        return this.request('POST', '/logout/');
    },

    getPersonas() { return this.request('GET', '/personas/'); },
    getPersona(id) { return this.request('GET', `/personas/${id}/`); },
    createPersona(data) { return this.request('POST', '/personas/', data); },
    updatePersona(id, data) { return this.request('PUT', `/personas/${id}/`, data); },
    deletePersona(id) { return this.request('DELETE', `/personas/${id}/`); },

    getNotas() { return this.request('GET', '/notas/'); },
    getNota(id) { return this.request('GET', `/notas/${id}/`); },
    createNota(mensaje) { return this.request('POST', '/notas/', { mensaje }); },
    updateNota(id, mensaje) { return this.request('PUT', `/notas/${id}/`, { mensaje }); },
    deleteNota(id) { return this.request('DELETE', `/notas/${id}/`); },
};
