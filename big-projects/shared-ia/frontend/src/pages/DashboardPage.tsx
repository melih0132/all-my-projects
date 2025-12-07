import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';
import { getSocket } from '@/lib/socket';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, Bell, Check, X } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { Socket } from 'socket.io-client';

interface Room {
  id: string;
  name: string;
  ai_context: string;
  creator_id: string;
  created_at: string;
  member_count?: number;
  last_message_at?: string;
}

interface Invitation {
  id: string;
  room_id: string;
  room_name: string;
  sender_id: string;
  sender_username: string;
  status: 'pending' | 'accepted' | 'rejected';
  expires_at: string;
  created_at: string;
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { toast } = useToast();
  const [rooms, setRooms] = useState<Room[]>([]);
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    loadData();
    setupSocket();

    return () => {
      if (socket) {
        socket.off('new-invitation');
      }
    };
  }, []);

  const setupSocket = () => {
    const socketInstance = getSocket();
    setSocket(socketInstance);

    socketInstance.on('new-invitation', (invitation: Invitation) => {
      setInvitations((prev) => [invitation, ...prev]);
      toast({
        title: 'Nouvelle invitation',
        description: `${invitation.sender_username} vous a invité à rejoindre "${invitation.room_name}"`,
      });
    });
  };

  const loadData = async () => {
    try {
      const [roomsResponse, invitationsResponse] = await Promise.all([
        api.get('/api/rooms'),
        api.get('/api/invitations/pending'),
      ]);
      setRooms(roomsResponse.data.rooms);
      setInvitations(invitationsResponse.data.invitations || []);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRoom = () => {
    navigate('/rooms/new');
  };

  const handleRoomClick = (roomId: string) => {
    navigate(`/rooms/${roomId}`);
  };

  const handleAcceptInvitation = async (invitationId: string) => {
    try {
      await api.post(`/api/invitations/${invitationId}/accept`);
      const invitation = invitations.find((inv) => inv.id === invitationId);
      if (invitation) {
        navigate(`/rooms/${invitation.room_id}`);
      }
      setInvitations((prev) => prev.filter((inv) => inv.id !== invitationId));
      toast({
        title: 'Invitation acceptée',
        description: 'Vous avez rejoint la conversation',
        variant: 'success',
      });
    } catch (err: any) {
      toast({
        title: 'Erreur',
        description: err.response?.data?.error || 'Impossible d\'accepter l\'invitation',
        variant: 'destructive',
      });
    }
  };

  const handleRejectInvitation = async (invitationId: string) => {
    try {
      await api.post(`/api/invitations/${invitationId}/reject`);
      setInvitations((prev) => prev.filter((inv) => inv.id !== invitationId));
      toast({
        title: 'Invitation refusée',
        variant: 'default',
      });
    } catch (err: any) {
      toast({
        title: 'Erreur',
        description: err.response?.data?.error || 'Impossible de refuser l\'invitation',
        variant: 'destructive',
      });
    }
  };

  const isInvitationExpired = (expiresAt: string) => {
    return new Date(expiresAt) < new Date();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl font-semibold">Shared IA</h1>
            <div className="flex items-center space-x-4">
              {invitations.length > 0 && (
                <Badge variant="default" className="flex items-center gap-1">
                  <Bell className="h-3 w-3" />
                  {invitations.length}
                </Badge>
              )}
              <span className="text-sm text-gray-600">Bonjour, {user?.username}</span>
              <Button variant="outline" onClick={logout}>
                Déconnexion
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Invitations */}
        {invitations.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Invitations en attente ({invitations.length})
            </h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {invitations.map((invitation) => {
                const expired = isInvitationExpired(invitation.expires_at);
                return (
                  <Card key={invitation.id} className="border-blue-200">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="text-base">{invitation.room_name}</CardTitle>
                          <CardDescription className="mt-1">
                            Invité par {invitation.sender_username}
                          </CardDescription>
                        </div>
                        {expired && (
                          <Badge variant="destructive" className="text-xs">
                            Expirée
                          </Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          onClick={() => handleAcceptInvitation(invitation.id)}
                          disabled={expired}
                          className="flex-1"
                        >
                          <Check className="h-4 w-4 mr-1" />
                          Accepter
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleRejectInvitation(invitation.id)}
                          className="flex-1"
                        >
                          <X className="h-4 w-4 mr-1" />
                          Refuser
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        )}

        {/* Rooms */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Mes conversations</h2>
          <Button onClick={handleCreateRoom}>
            <Plus className="mr-2 h-4 w-4" />
            Nouvelle conversation
          </Button>
        </div>

        {loading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4" />
                  <Skeleton className="h-4 w-full mt-2" />
                  <Skeleton className="h-4 w-2/3 mt-2" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-4 w-1/2" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600">{error}</p>
          </div>
        ) : rooms.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">Aucune conversation pour le moment</p>
            <Button onClick={handleCreateRoom}>
              <Plus className="mr-2 h-4 w-4" />
              Créer une conversation
            </Button>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {rooms.map((room) => (
              <Card
                key={room.id}
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleRoomClick(room.id)}
              >
                <CardHeader>
                  <CardTitle className="truncate">{room.name}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    {room.ai_context}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-500">
                    {room.member_count || 0} membre(s)
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
