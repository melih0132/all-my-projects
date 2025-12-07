import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const createRoomSchema = z.object({
  name: z.string().max(100).optional(),
  aiContext: z.string().min(1, 'Le contexte IA est requis'),
});

type CreateRoomFormData = z.infer<typeof createRoomSchema>;

export default function CreateRoomPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateRoomFormData>({
    resolver: zodResolver(createRoomSchema),
  });

  const onSubmit = async (data: CreateRoomFormData) => {
    setError(null);
    setLoading(true);

    try {
      const response = await api.post('/api/rooms', data);
      navigate(`/rooms/${response.data.room.id}`);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de la creation de la room');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center">
            <Link to="/dashboard" className="flex items-center text-gray-600 hover:text-gray-900">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Nouvelle conversation</CardTitle>
            <CardDescription>
              Creez une nouvelle conversation avec l'IA. Definissez le contexte et le role de l'IA.
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit(onSubmit)}>
            <CardContent className="space-y-4">
              {error && (
                <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                  {error}
                </div>
              )}
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-medium">
                  Nom de la conversation (optionnel)
                </label>
                <Input
                  id="name"
                  placeholder="Ma conversation"
                  {...register('name')}
                  disabled={loading}
                />
                {errors.name && (
                  <p className="text-sm text-red-600">{errors.name.message}</p>
                )}
                <p className="text-xs text-gray-500">
                  Si vide, un nom sera genere automatiquement
                </p>
              </div>
              <div className="space-y-2">
                <label htmlFor="aiContext" className="text-sm font-medium">
                  Contexte IA <span className="text-red-500">*</span>
                </label>
                <textarea
                  id="aiContext"
                  className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Tu es un assistant developpeur specialise en React. Tu aides l'equipe a resoudre des problemes techniques..."
                  {...register('aiContext')}
                  disabled={loading}
                />
                {errors.aiContext && (
                  <p className="text-sm text-red-600">{errors.aiContext.message}</p>
                )}
                <p className="text-xs text-gray-500">
                  Decrivez le role et le contexte de l'IA pour cette conversation
                </p>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => navigate('/dashboard')} disabled={loading}>
                Annuler
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Creation...' : 'Creer la conversation'}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </main>
    </div>
  );
}

