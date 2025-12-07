-- Schéma de base de données pour l'application de chat IA collaboratif

-- Table Users
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(20) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table Rooms
CREATE TABLE IF NOT EXISTS rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  ai_context TEXT NOT NULL,
  creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table RoomMembers
CREATE TABLE IF NOT EXISTS room_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(100) NULL,
  joined_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(room_id, user_id)
);

-- Table Messages
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
  type VARCHAR(20) NOT NULL CHECK (type IN ('user', 'ai', 'system')),
  status VARCHAR(30) NOT NULL CHECK (status IN ('sent', 'pending_validation', 'validated', 'rejected', 'error')),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  edited_at TIMESTAMP NULL
);

-- Table MessageValidations
CREATE TABLE IF NOT EXISTS message_validations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  member_id UUID NOT NULL REFERENCES room_members(id) ON DELETE CASCADE,
  action VARCHAR(20) NOT NULL CHECK (action IN ('validated', 'added', 'rejected')),
  addition TEXT NULL,
  comment TEXT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(message_id, member_id)
);

-- Table MessageConflicts
CREATE TABLE IF NOT EXISTS message_conflicts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL CHECK (status IN ('voting', 'resolved')),
  winner_id UUID NULL REFERENCES messages(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  resolved_at TIMESTAMP NULL
);

-- Table ConflictMessages (liaison many-to-many)
CREATE TABLE IF NOT EXISTS conflict_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conflict_id UUID NOT NULL REFERENCES message_conflicts(id) ON DELETE CASCADE,
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  UNIQUE(conflict_id, message_id)
);

-- Table Votes
CREATE TABLE IF NOT EXISTS votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conflict_id UUID NOT NULL REFERENCES message_conflicts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(conflict_id, user_id)
);

-- Table Invitations
CREATE TABLE IF NOT EXISTS invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'accepted', 'rejected')),
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_room_members_room_id ON room_members(room_id);
CREATE INDEX IF NOT EXISTS idx_room_members_user_id ON room_members(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_room_id ON messages(room_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_message_validations_message_id ON message_validations(message_id);
CREATE INDEX IF NOT EXISTS idx_message_validations_member_id ON message_validations(member_id);
CREATE INDEX IF NOT EXISTS idx_invitations_recipient_id ON invitations(recipient_id);
CREATE INDEX IF NOT EXISTS idx_invitations_status ON invitations(status);
CREATE INDEX IF NOT EXISTS idx_invitations_expires_at ON invitations(expires_at);
CREATE INDEX IF NOT EXISTS idx_votes_conflict_id ON votes(conflict_id);
CREATE INDEX IF NOT EXISTS idx_votes_user_id ON votes(user_id);

