import React, { useState } from 'react';

const UserProfile = ({ username, age }) => {
    const [isEditing, setIsEditing] = useState(false);

    const handleSave = () => {
        console.log(`Saving profile for ${username}`);
        setIsEditing(false);
    };

    return (
        <div className="profile-container">
            <h1>{username}'s Profile</h1>
            {isEditing ? (
                <button onClick={handleSave}>Save</button>
            ) : (
                <button onClick={() => setIsEditing(true)}>Edit</button>
            )}
        </div>
    );
};

export default UserProfile;
