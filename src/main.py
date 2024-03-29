from jaya import Jaya
from score_calculator import ScoreCalculator
from data_access import Logger, ImageLoader
import pathos.multiprocessing
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import AdaBoostClassifier

# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF
# from sklearn.neural_network import MLPClassifier
# from sklearn.neural_network import MLPClassifier
# from sklearn.tree import DecisionTreeClassifier


if __name__ == '__main__':
    PROCESS_NUMBERS = 2
    POPULATION_SIZE = 30
    NUMBER_OF_GENERATIONS = 100
    NUMBER_OF_IMAGES = 20
    PLOT_NAME = "CLL_MCL_ADA_BOOST_2"
    SEED_K_FOLD = 123456
    K_SPLITS = 3
    SCORING = 'roc_auc'  # 'accuracy'
    DATABASES = [
       # "data/FL",
        "./data/CLL",
        "./data/MCL"
    ]
    CLASSIFIERS = {
        # "Nearest Neighbors": lambda:  KNeighborsClassifier(5),
        # "Linear SVM": lambda: SVC(kernel="linear", C=0.025,cache_size=7000, random_state=SEED_K_FOLD, gamma="scale"),
        # "Sigmoid SVM": lambda: SVC(kernel="sigmoid", C=0.025, random_state=SEED_K_FOLD),
        # "RBF SVM": lambda: SVC(kernel="rbf", C=0.025, random_state=SEED_K_FOLD),
        # "Gaussian Process": lambda:  GaussianProcessClassifier(1.0 * RBF(1.0), random_state=SEED_K_FOLD),
        # "Decision Tree": lambda: DecisionTreeClassifier(random_state=SEED_K_FOLD),
        #"Random Forest": lambda: RandomForestClassifier(random_state=SEED_K_FOLD),
        # "Neural Net": lambda: MLPClassifier(alpha=1, random_state=SEED_K_FOLD),
        "AdaBoost": lambda: AdaBoostClassifier(random_state=SEED_K_FOLD),
    }

    logger = Logger(title=PLOT_NAME)
    poolMapper = pathos.multiprocessing.ProcessingPool(PROCESS_NUMBERS)
    image_loader = ImageLoader(directories_path=DATABASES,
                               images_number=NUMBER_OF_IMAGES
                               )
    stratified_k_fold = StratifiedKFold(n_splits=K_SPLITS,
                                        shuffle=True,
                                        random_state=SEED_K_FOLD
                                        )
    scoreCalculator = ScoreCalculator(image_loader=image_loader,
                                      cross_validation_strategy=stratified_k_fold,
                                      scoring=SCORING,
                                      classifiers=CLASSIFIERS,
                                      logger=logger
                                      )
    jaya = Jaya(population_size=POPULATION_SIZE,
                generations_number=NUMBER_OF_GENERATIONS,
                score_calculator=scoreCalculator,
                logger=logger,
                pool=poolMapper
                )

    jaya.execute()
