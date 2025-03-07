import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import { type ApiError, type ChurchUnionCreate, UnionsService
    
 } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"

interface AddChurchUnionProps {
    isOpen: boolean
    onClose: () => void
}

const AddChurchUnion = ({ isOpen, onClose }: AddChurchUnionProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<ChurchUnionCreate>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            name: "",
            description: "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: ChurchUnionCreate) =>
            UnionsService.createUnion({ requestBody: data }),
        onSuccess: () => {
            showToast("Success!", "Church Union created successfully.", "success")
            reset()
            onClose()
        },
        onError: (err: ApiError) => {
            const errDetail = (err.body as any)?.detail
            showToast("Something went wrong.", `${errDetail}`, "error")
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ["churchUnions"] })
        },
    })

    const onSubmit: SubmitHandler<ChurchUnionCreate> = (data) => {
        mutation.mutate(data)
    }

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: "sm", md: "md" }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                    <ModalHeader>Add Church Union</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl isRequired isInvalid={!!errors.name}>
                            <FormLabel htmlFor="name">Name</FormLabel>
                            <Input
                                id="name"
                                {...register("name", {
                                    required: "Name is required.",
                                })}
                                placeholder="Name"
                                type="text"
                            />
                            {errors.name && (
                                <FormErrorMessage>{errors.name.message}</FormErrorMessage>
                            )}
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor="description">Description</FormLabel>
                            <Input
                                id="description"
                                {...register("description")}
                                placeholder="Description"
                                type="text"
                            />
                        </FormControl>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button variant="primary" type="submit" isLoading={isSubmitting}>
                            Save
                        </Button>
                        <Button onClick={onClose}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default AddChurchUnion