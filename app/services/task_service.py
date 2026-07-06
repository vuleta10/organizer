from app.models.task import Task

class TaskService:

    def __init__(
        self,
        task_repository,
        user_repository
    ):
    #kreiraj task repo i user repo objekte
        self.task_repository = task_repository
        self.user_repository = user_repository
    
    #Provera da li user postoji  
    def create_task(
        self,
        user_id,
        task_text,
        datum
    ):

        user = (
            self.user_repository #dohvati usera iz user repo
            .get_by_id(user_id)
        )

        if not user:
            raise ValueError(
                "User not found." # ako ne postoji vrati poruku
            )
        #kreiraj task objekat
        task = Task(
            user_id=user_id,
            task=task_text,
            datum=datum,
            done=False
        )
        # vrati task objekat
        return (
            self.task_repository
            .create(task)
        )
    # vrati sve taskove za usera
    def get_tasks_by_user(
        self,
        user_id
    ):
        
        return (
            self.task_repository
            .get_tasks_by_user(user_id) # zove metod iz task repo koji vraća sve taskove za usera
        )
     # vrati taskove za datum za korisnika
     
    def get_tasks_by_date(
        self,
        user_id,
        datum
    ):

        return (
            self.task_repository # zove metod iz task repo koji vraća sve taskove za datum za tog usera
            .get_tasks_by_date(
                user_id,
                datum
            )
        )
    #Ažuriranje taska
    def update_task(
        self,
        task_id,
        task_text,
        datum,
        done
    ):

        task = (
            self.task_repository #dohvata task iz task repo na osnovu id
            .get_by_id(task_id)
        )

        if not task:
            raise ValueError(
                "Task not found." #ako ne postoji vraća poruku o grešci
            )
        # postavljamo nove vrednosti za task
        task.task = task_text
        task.datum = datum
        task.done = done

        self.task_repository.update() #zovemo metod iz task repo za update

        return task 
        
    # brisanje taska
    def delete_task(
        self,
        task_id
    ):

        task = (
            self.task_repository #zove metod iz task repo za brisanje task
            .delete(task_id)
        )

        if not task:
            raise ValueError(
                "Task not found." #vraća poruku o grešci ako ne nađe task
            )

        return task