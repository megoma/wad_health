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
import { UnionsService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

const unionsSearchSchema = z.object({
    page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/unions")({
    component: Unions,
    validateSearch: (search) => unionsSearchSchema.parse(search),
})

const PER_PAGE = 5

function getUnionsQueryOptions({ page }: { page: number }) {
    return {
        queryFn: () =>
            UnionsService.readUnions({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
        queryKey: ["unions", { page }],
    }
}

function UnionsTable() {
    const queryClient = useQueryClient()
    const { page } = Route.useSearch()
    const navigate = useNavigate({ from: Route.fullPath })
    const setPage = (page: number) =>
        navigate({ search: (prev) => ({ ...prev, page }) })

    const {
        data: unions,
        isPending,
        isPlaceholderData,
    } = useQuery({
        ...getUnionsQueryOptions({ page }),
        placeholderData: (prevData) => prevData,
    })

    const hasNextPage = !isPlaceholderData && unions?.data.length === PER_PAGE
    const hasPreviousPage = page > 1

    useEffect(() => {
        if (hasNextPage) {
            queryClient.prefetchQuery(getUnionsQueryOptions({ page: page + 1 }))
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
                            <Th>Description</Th>
                            <Th>Actions</Th>
                        </Tr>
                    </Thead>
                    {isPending ? (
                        <Tbody>
                            {new Array(5).fill(null).map((_, index) => (
                                <Tr key={index}>
                                    {new Array(4).fill(null).map((_, index) => (
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
                            {unions?.data.map((union) => (
                                <Tr key={union.id} opacity={isPlaceholderData ? 0.5 : 1}>
                                    <Td>{union.id}</Td>
                                    <Td>{union.name}</Td>
                                    <Td color={!union.description ? "ui.dim" : "inherit"}>
                                        {union.description || "N/A"}
                                    </Td>
                                    <Td>
                                        <ActionsMenu type={"Union"} value={union} />
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

function Unions() {
    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
                Unions Management
            </Heading>

            <Navbar type={"Union"} />
            <UnionsTable />
        </Container>
    )
}