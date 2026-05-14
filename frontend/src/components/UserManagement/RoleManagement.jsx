import React, { useState, useEffect } from 'react';
import { getUserRoles, updateUserRole } from '../../services/api';

const ROLES = ['admin', 'analyst', 'clinician'];

const ROLE_COLOR = {
    admin:     { bg: '#fff1f0', color: '#cf1322', border: '#ffa39e' },
    analyst:   { bg: '#e6f7ff', color: '#0050b3', border: '#91d5ff' },
    clinician: { bg: '#f6ffed', color: '#389e0d', border: '#b7eb8f' },
};

const RoleManagement = () => {
    const [users, setUsers] = useState([]);
    const [pending, setPending] = useState({});   // userId -> selected role
    const [saving, setSaving] = useState({});      // userId -> bool
    const [saved, setSaved] = useState({});        // userId -> bool (flash)
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const load = async () => {
        setLoading(true);
        setError(null);
        try {
            const users = await getUserRoles();
            setUsers(users || []);
            const init = {};
            (users || []).forEach((u) => { init[u.id] = u.role; });
            setPending(init);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to fetch user roles');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { load(); }, []);

    const handleSave = async (userId) => {
        setSaving((s) => ({ ...s, [userId]: true }));
        try {
            await updateUserRole(userId, pending[userId]);
            setUsers((prev) =>
                prev.map((u) => u.id === userId ? { ...u, role: pending[userId] } : u)
            );
            setSaved((s) => ({ ...s, [userId]: true }));
            setTimeout(() => setSaved((s) => ({ ...s, [userId]: false })), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to update role');
        } finally {
            setSaving((s) => ({ ...s, [userId]: false }));
        }
    };

    const isDirty = (user) => pending[user.id] !== user.role;

    if (loading) return <div style={{ padding: '20px' }}>Loading…</div>;

    return (
        <div style={s.wrap}>
            <h2>Manage User Roles</h2>
            <p style={s.muted}>Change a user's role and click <strong>Save</strong> to apply.</p>

            {error && (
                <div style={s.errorBox}>
                    <p style={{ margin: 0, color: '#cf1322' }}>{error}</p>
                    <button style={s.retryBtn} onClick={load}>Retry</button>
                </div>
            )}

            {!error && users.length === 0 && (
                <p style={s.muted}>No users found.</p>
            )}

            {users.length > 0 && (
                <div style={s.tableWrap}>
                    <table style={s.table}>
                        <thead>
                            <tr>
                                <th style={s.th}>Username</th>
                                <th style={s.th}>Email</th>
                                <th style={s.th}>Current Role</th>
                                <th style={s.th}>New Role</th>
                                <th style={s.th}>Status</th>
                                <th style={s.th}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user, i) => {
                                const rc = ROLE_COLOR[user.role] || ROLE_COLOR.clinician;
                                const isSaving = saving[user.id];
                                const wasSaved = saved[user.id];
                                const dirty = isDirty(user);
                                return (
                                    <tr key={user.id} style={i % 2 === 0 ? s.rowEven : s.rowOdd}>
                                        <td style={s.td}><strong>{user.username}</strong></td>
                                        <td style={{ ...s.td, color: '#666' }}>{user.email}</td>
                                        <td style={s.td}>
                                            <span style={{ ...s.roleBadge, backgroundColor: rc.bg, color: rc.color, border: `1px solid ${rc.border}` }}>
                                                {user.role}
                                            </span>
                                        </td>
                                        <td style={s.td}>
                                            <select
                                                style={s.select}
                                                value={pending[user.id] ?? user.role}
                                                onChange={(e) => setPending((p) => ({ ...p, [user.id]: e.target.value }))}
                                            >
                                                {ROLES.map((r) => (
                                                    <option key={r} value={r}>{r}</option>
                                                ))}
                                            </select>
                                        </td>
                                        <td style={s.td}>
                                            {wasSaved && <span style={{ color: '#52c41a', fontSize: '13px' }}>✓ Saved</span>}
                                            {!wasSaved && dirty && <span style={{ color: '#faad14', fontSize: '13px' }}>Unsaved</span>}
                                            {!wasSaved && !dirty && <span style={{ color: '#bbb', fontSize: '13px' }}>—</span>}
                                        </td>
                                        <td style={s.td}>
                                            <button
                                                style={{
                                                    ...s.saveBtn,
                                                    backgroundColor: dirty ? '#1890ff' : '#d9d9d9',
                                                    cursor: dirty && !isSaving ? 'pointer' : 'not-allowed',
                                                }}
                                                disabled={!dirty || isSaving}
                                                onClick={() => handleSave(user.id)}
                                            >
                                                {isSaving ? 'Saving…' : 'Save'}
                                            </button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#666', marginBottom: '16px' },
    errorBox: {
        padding: '12px 16px', marginBottom: '16px',
        backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    },
    retryBtn: {
        padding: '4px 12px', border: '1px solid #ffccc7', borderRadius: '4px',
        backgroundColor: '#fff', cursor: 'pointer', fontSize: '13px',
    },
    tableWrap: { overflowX: 'auto' },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '14px' },
    th: {
        padding: '10px 14px', backgroundColor: '#fafafa',
        border: '1px solid #e8e8e8', fontWeight: 600, textAlign: 'left',
    },
    td: { padding: '8px 14px', border: '1px solid #e8e8e8' },
    rowEven: { backgroundColor: '#fff' },
    rowOdd:  { backgroundColor: '#fafafa' },
    roleBadge: {
        padding: '2px 10px', borderRadius: '10px',
        fontSize: '12px', fontWeight: 600,
    },
    select: {
        padding: '5px 8px', border: '1px solid #d9d9d9',
        borderRadius: '4px', fontSize: '13px',
    },
    saveBtn: {
        padding: '5px 14px', color: '#fff', border: 'none',
        borderRadius: '4px', fontSize: '13px',
    },
};

export default RoleManagement;
