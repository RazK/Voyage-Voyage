"""Token encryption utilities using AES-GCM."""
import base64
import secrets
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from app.core.config import settings


class EncryptionError(Exception):
    """Raised when encryption/decryption fails."""

    pass


class TokenEncryption:
    """AES-GCM encryption for refresh tokens."""

    def __init__(self, key: Optional[str] = None):
        """
        Initialize token encryption.

        Args:
            key: Base64-encoded 32-byte key. If None, uses TOKEN_ENCRYPTION_KEY from settings.
        """
        encryption_key = key or settings.token_encryption_key
        if not encryption_key:
            raise ValueError("TOKEN_ENCRYPTION_KEY must be set in environment variables")

        try:
            # Decode base64 key to bytes
            key_bytes = base64.b64decode(encryption_key)
            if len(key_bytes) != 32:
                raise ValueError(f"Encryption key must be 32 bytes (got {len(key_bytes)})")
        except Exception as e:
            raise ValueError(f"Invalid TOKEN_ENCRYPTION_KEY format: {e}") from e

        self._aesgcm = AESGCM(key_bytes)
        self._nonce_length = 12  # 12 bytes for GCM

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext token.

        Args:
            plaintext: The token to encrypt.

        Returns:
            Base64-encoded string containing nonce + ciphertext.

        Raises:
            EncryptionError: If encryption fails.
        """
        try:
            # Generate random nonce
            nonce = secrets.token_bytes(self._nonce_length)

            # Encrypt
            plaintext_bytes = plaintext.encode("utf-8")
            ciphertext = self._aesgcm.encrypt(nonce, plaintext_bytes, None)

            # Combine nonce + ciphertext and base64 encode
            encrypted = nonce + ciphertext
            return base64.b64encode(encrypted).decode("utf-8")
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {e}") from e

    def decrypt(self, encrypted_token: str) -> str:
        """
        Decrypt an encrypted token.

        Args:
            encrypted_token: Base64-encoded string containing nonce + ciphertext.

        Returns:
            Decrypted plaintext token.

        Raises:
            EncryptionError: If decryption fails or token is invalid.
        """
        try:
            # Decode base64
            encrypted_bytes = base64.b64decode(encrypted_token)

            # Extract nonce and ciphertext
            if len(encrypted_bytes) < self._nonce_length:
                raise EncryptionError("Invalid encrypted token format")

            nonce = encrypted_bytes[: self._nonce_length]
            ciphertext = encrypted_bytes[self._nonce_length :]

            # Decrypt
            plaintext_bytes = self._aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext_bytes.decode("utf-8")
        except InvalidTag:
            raise EncryptionError("Decryption failed: invalid or tampered token") from None
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {e}") from e


# Global instance (initialized on first use)
_token_encryption: Optional[TokenEncryption] = None


def get_token_encryption() -> TokenEncryption:
    """Get or create the global token encryption instance."""
    global _token_encryption
    if _token_encryption is None:
        _token_encryption = TokenEncryption()
    return _token_encryption


def encrypt_token(plaintext: str) -> str:
    """Convenience function to encrypt a token."""
    return get_token_encryption().encrypt(plaintext)


def decrypt_token(encrypted_token: str) -> str:
    """Convenience function to decrypt a token."""
    return get_token_encryption().decrypt(encrypted_token)

