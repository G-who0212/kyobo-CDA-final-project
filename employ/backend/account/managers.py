from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email=None, name=None, company=None, password=None, **extra_fields):
        if email is None:
            raise TypeError("Users must have a email.")
        if name is None:
            raise TypeError("Users must have a name.")
        if password is None:
            raise TypeError("Users must have a password.")
        if company is None:
            raise TypeError("Users must have a comapany.")

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            company = company,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, company, password=None, **extra_fields):    
        user = self.create_user(email, name, company, password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user