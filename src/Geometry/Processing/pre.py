from ..healing.baseline_healing import baseline_heal
from ..validation.baseline_validation import baseline_validation_check


def preprocess_solid_volume_for_convexhull_difference(solid_volume):
    print("\nPreprocessing solid volume mesh for convex hull difference algorithm...")

    validation_successfull_msg = "✅ Input solid volume mesh is valid and represents a watertight volume. No healing needed."
    validation_not_successfull_msg = (
        "❌ Input solid volume mesh is not valid. Healing required."
    )
    healing_successfull_msg = (
        "✅ Input solid volume mesh has been successfully healed to a valid mesh."
    )
    healing_not_successfull_msg = "❌ Input solid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm."

    if baseline_validation_check(solid_volume):
        print(validation_successfull_msg)
        return True

    print(validation_not_successfull_msg)
    baseline_heal(solid_volume)

    if baseline_validation_check(solid_volume):
        print(healing_successfull_msg)
        return True

    print(healing_not_successfull_msg)
    return None
