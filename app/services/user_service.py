from app.models.user import User


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository # kreiramo objekat user_repository
    # kreiramo metod register    
    def register(
        self,
        username,
        password
    ):
        #provera da li postoji user kog registrujemo
        existing_user = (
            self.user_repository
            .get_by_username(username)  #dohvatamo usera iz user repo zovemo metod get_by_username
        )

        if existing_user:
            raise ValueError(
                "Username already exists." #vraćamo poruku o grešci
            )
        #pravimo user objekat, dodeljujemo username i pwd
        user = User(
            username=username,
            password=password
        )
        #zovemo metod iz user repo koji kreira usera
        return self.user_repository.create( 
            user
        )
    # definišemo login metod   
    def login(
        self,
        username,
        password
    ):

        user = (
            self.user_repository
            .get_by_username(username) #zovemo metod za dohvatanje usera iz user repo
        )

        if not user:
            raise ValueError(
                "User not found." #ako ne postoji vraćamo poruku o grešci
            )
        # provera pwd i vraćanje poruke o grešci
        if user.password != password:
            raise ValueError(
                "Invalid password."
            )

        return user # vraćamo objekat user ako je sve ok
    # definicija metoda za promenu pwd
    def change_password(
        self,
        username,
        old_password,
        new_password
    ):

        user = (
            self.user_repository
            .get_by_username(username) # zovemo metod za dohvatanje usera u user repo
        )

        if not user:
            raise ValueError(
                "User not found."  #ako ne postoji vraćamo poruku o grešci
            )

        if user.password != old_password:
            raise ValueError(
                "Wrong password." #ako ne valja pwd vraćamo poruku o grešci
            )

        user.password = new_password  #postavljamo novi pwd

        self.user_repository.update() #zovemo metod za ažuriranje usera u user repo

        return user #vraćamo user objekat