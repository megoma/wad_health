import { Box, Container, Text, SimpleGrid, Card, CardBody, Icon, Heading, Stack, Divider } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { FaUsers, FaBox, FaCogs, FaChartBar, FaWeightHanging, FaHeartbeat, FaStethoscope, FaChartLine, FaMars, FaVenus } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

import useAuth from "../../hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  const sampleData = [
    { date: '2024-01-01', value: 70 },
    { date: '2024-02-01', value: 72 },
    { date: '2024-03-01', value: 71 },
    { date: '2024-04-01', value: 69 },
    { date: '2024-05-01', value: 68 }
  ];

  return (
    <>
      <Container maxW="full">
        <Box pt={12} m={4}>
        <Heading mb={6}>Tableau de bord</Heading>
          <Text fontSize="2xl">
            Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
          </Text>
          <Text>Welcome back, nice to see you again!</Text>

          {/* Heading principal */}
          <SimpleGrid
        columns={{ base: 1, md: 2, lg: 4 }} // 1 colonne sur mobile, 2 sur tablette, 4 sur desktop
        spacing={4}
        wrap="wrap" // Permet de revenir à la ligne si nécessaire
      >
        {/* Première carte */}
        <Card>
          <CardBody>
            <Icon as={FaUsers} w={10} h={10} color="teal.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">245</Text>
            <Text>Utilisateurs</Text>
          </CardBody>
        </Card>

        {/* Deuxième carte */}
        <Card>
          <CardBody>
            <Icon as={FaBox} w={10} h={10} color="blue.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">120</Text>
            <Text>Produits</Text>
          </CardBody>
        </Card>

        {/* Troisième carte */}
        <Card>
          <CardBody>
            <Icon as={FaCogs} w={10} h={10} color="orange.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">76</Text>
            <Text>Paramètres</Text>
          </CardBody>
        </Card>

        {/* Quatrième carte */}
        <Card>
          <CardBody>
            <Icon as={FaChartBar} w={10} h={10} color="purple.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">15</Text>
            <Text>Statistiques</Text>
          </CardBody>
        </Card>
      </SimpleGrid>
        </Box>
        <Box p={4}>
      {/* Heading principal */}
      <Heading mb={6}>Métriques de Santé</Heading>

      {/* Conteneur des cartes */}
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 4 }} // 1 colonne sur mobile, 2 sur tablette, 4 sur desktop
        spacing={4}
        wrap="wrap" // Permet de revenir à la ligne si nécessaire
      >
        {/* Carte du poids */}
        <Card>
          <CardBody>
            <Icon as={FaWeightHanging} w={10} h={10} color="teal.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">68 kg</Text>
            <Text>Poids</Text>
          </CardBody>
        </Card>

        {/* Carte de la tension artérielle */}
        <Card>
          <CardBody>
            <Icon as={FaHeartbeat} w={10} h={10} color="red.500" mb={4} />
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={sampleData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
            <Text>Tension artérielle (mmHg)</Text>
          </CardBody>
        </Card>

        {/* Carte de l'indice de masse corporelle (IMC) */}
        <Card>
          <CardBody>
            <Icon as={FaStethoscope} w={10} h={10} color="orange.500" mb={4} />
            <Text fontSize="2xl" fontWeight="bold">23.5</Text>
            <Text>IMC</Text>
          </CardBody>
        </Card>

        {/* Carte du temps moyen de stress */}
        <Card>
          <CardBody>
            <Icon as={FaChartLine} w={10} h={10} color="purple.500" mb={4} />
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={sampleData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
            <Text>Temps moyen de stress (min)</Text>
          </CardBody>
        </Card>

        {/* Carte de la répartition par sexe */}
        <Card>
          <CardBody>
            <Stack direction="row" spacing={4} justify="center">
              <Box textAlign="center">
                <Icon as={FaMars} w={10} h={10} color="blue.500" />
                <Text fontSize="2xl" fontWeight="bold">120</Text>
                <Text>Hommes</Text>
              </Box>
              <Divider orientation="vertical" />
              <Box textAlign="center">
                <Icon as={FaVenus} w={10} h={10} color="pink.500" />
                <Text fontSize="2xl" fontWeight="bold">130</Text>
                <Text>Femmes</Text>
              </Box>
            </Stack>
          </CardBody>
        </Card>
      </SimpleGrid>
    </Box>
      </Container>
    </>
  )
}
