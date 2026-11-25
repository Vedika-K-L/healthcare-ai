export const ok = (res, data, message = 'Success', status = 200) => res.status(status).json({ success: true, message, data });
export const fail = (res, status, message, errors) => res.status(status).json({ success: false, message, ...(errors ? { errors } : {}) });
export const pageOf = query => ({ page: Math.max(1, Number(query.page) || 1), limit: Math.min(50, Math.max(1, Number(query.limit) || 20)) });
