import React, { useState, useEffect } from 'react';
import { getUserRoles, updateUserRole } from '../../services/api';

const RoleManagement = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserRoles = async () => {
            try {
                const response = await getUserRoles();
                setUsers(response.data);
            } catch (err) {
                setError('Failed to fetch user roles');
            } finally {
                setLoading(false);
            }
        };

        fetchUserRoles();
    }, []);

    const handleRoleChange = async (userId, newRole) => {
        try {
            await updateUserRole(userId, newRole);
            setUsers(users.map(user => (user.id === userId ? { ...user, role: newRole } : user)));
        } catch (err) {
            setError('Failed to update user role');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h2>Manage User Roles</h2>
            <table>
                <thead>
                    <tr>
                        <th>User</th>
                        <th>Role</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.name}</td>
                            <td>
                                <select
                                    value={user.role}
                                    onChange={(e) => handleRoleChange(user.id, e.target.value)}
                                >
                                    <option value="admin">Admin</option>
                                    <option value="analyst">Analyst</option>
                                    <option value="clinician">Clinician</option>
                                </select>
                            </td>
                            <td>
                                <button onClick={() => handleRoleChange(user.id, user.role)}>Update</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RoleManagement;