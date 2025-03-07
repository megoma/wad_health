import { z } from "zod"
import {
    Button,
    Container,
    Flex,
    Heading,
    Skeleton,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"

import { useEffect } from "react"
import { ConferencesService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

const conferencesSearchSchema = z.object({
    page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/conferences")({
    component: Conferences,
    validateSearch: (search) => conferencesSearchSchema.parse(search),
})

const PER_PAGE = 5

function getConferencesQueryOptions({ page }: { page: number }) {
    return {
        queryFn: () =>
            ConferencesService.readConferences({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
        queryKey: ["conferences", { page }],
    }
}

function ConferencesTable() {
    const queryClient = useQueryClient()
    const { page } = Route.useSearch()
    const navigate = useNavigate({ from: Route.fullPath })
    const setPage = (page: number) =>
        navigate({ search: (prev) => ({ ...prev, page }) })

    const {
        data: conferences,
        isPending,
        isPlaceholderData,
    } = useQuery({
        ...getConferencesQueryOptions({ page }),
        placeholderData: (prevData) => prevData,
    })

    const hasNextPage = !isPlaceholderData && conferences?.data.length === PER_PAGE
    const hasPreviousPage = page > 1

    useEffect(() => {
        if (hasNextPage) {
            queryClient.prefetchQuery(getConferencesQueryOptions({ page: page + 1 }))
        }
    }, [page, queryClient])

    return (
        <>
            <TableContainer>
                <Table size={{ base: "sm", md: "md" }}>
                    <Thead>
                        <Tr>
                            <Th>ID</Th>
                            <Th>Name</Th>
                            <Th>Address</Th>
                            <Th>Phone Number</Th>
                            <Th>Email</Th>
                            <Th>Website</Th>
                            <Th>Description</Th>
                            <Th>Actions</Th>
                        </Tr>
                    </Thead>
                    {isPending ? (
                        <Tbody>
                            {new Array(5).fill(null).map((_, index) => (
                                <Tr key={index}>
                                    {new Array(8).fill(null).map((_, index) => (
                                        <Td key={index}>
                                            <Flex>
                                                <Skeleton height="20px" width="20px" />
                                            </Flex>
                                        </Td>
                                    ))}
                                </Tr>
                            ))}
                        </Tbody>
                    ) : (
                        <Tbody>
                            {conferences?.data.map((conference) => (
                                <Tr key={conference.id} opacity={isPlaceholderData ? 0.5 : 1}>
                                    <Td>{conference.id}</Td>
                                    <Td>{conference.name}</Td>
                                    <Td>{conference.address}</Td>
                                    <Td>{conference.phone_number}</Td>
                                    <Td>{conference.email}</Td>
                                    <Td>{conference.website}</Td>
                                    <Td color={!conference.description ? "ui.dim" : "inherit"}>
                                        {conference.description || "N/A"}
                                    </Td>
                                    <Td>
                                        <ActionsMenu type={"Conference"} value={conference} />
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    )}
                </Table>
            </TableContainer>
            <Flex
                gap={4}
                alignItems="center"
                mt={4}
                direction="row"
                justifyContent="flex-end"
            >
                <Button onClick={() => setPage(page - 1)} isDisabled={!hasPreviousPage}>
                    Previous
                </Button>
                <span>Page {page}</span>
                <Button isDisabled={!hasNextPage} onClick={() => setPage(page + 1)}>
                    Next
                </Button>
            </Flex>
        </>
    )
}

function Conferences() {
    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
                Conferences Management
            </Heading>

            <Navbar type={"Conference"} />
            <ConferencesTable />
        </Container>
    )
}