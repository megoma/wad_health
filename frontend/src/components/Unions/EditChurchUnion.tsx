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

import {
    type ApiError,
    type ChurchUnionPublic,
    type ChurchUnionUpdate,
    UnionsService,
} from "../../client"
import useCustomToast from "../../hooks/useCustomToast"

interface EditChurchUnionProps {
    churchUnion: ChurchUnionPublic
    isOpen: boolean
    onClose: () => void
}

const EditChurchUnion = ({ churchUnion, isOpen, onClose }: EditChurchUnionProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
        register,
        handleSubmit,
        reset,
        formState: { isSubmitting, errors, isDirty },
    } = useForm<ChurchUnionUpdate>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: churchUnion,
    })

    const mutation = useMutation({
        mutationFn: (data: ChurchUnionUpdate) =>
            UnionsService.updateUnion({ id: churchUnion.id, requestBody: data }),
        onSuccess: () => {
            showToast("Success!", "Church Union updated successfully.", "success")
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

    const onSubmit: SubmitHandler<ChurchUnionUpdate> = async (data) => {
        mutation.mutate(data)
    }

    const onCancel = () => {
        reset()
        onClose()
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
                    <ModalHeader>Edit Church Union</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl isInvalid={!!errors.name}>
                            <FormLabel htmlFor="name">Name</FormLabel>
                            <Input
                                id="name"
                                {...register("name", {
                                    required: "Name is required",
                                })}
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
                        <Button
                            variant="primary"
                            type="submit"
                            isLoading={isSubmitting}
                            isDisabled={!isDirty}
                        >
                            Save
                        </Button>
                        <Button onClick={onCancel}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default EditChurchUnion