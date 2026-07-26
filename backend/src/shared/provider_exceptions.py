class ProviderException(Exception):
    """
    Erro relacionado a integrações externas.
    """

    def __init__(
        self,
        provider: str,
        message: str,
    ):

        self.provider = provider
        self.message = message

        super().__init__(
            f"{provider}: {message}"
        )