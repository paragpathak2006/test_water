from ..healing.baseline_healing import baseline_heal
from ..validation.baseline_validation import baseline_validation_check


def postprocess(fluid_volume):

    print("\nPostprocessing fluid volume mesh for convex hull difference algorithm...")

    validation_successfull_msg = "✅ Output fluid volume mesh is valid and represents a fluid volume. No healing needed."
    validation_not_successfull_msg = (
        "❌ Output fluid volume mesh is not valid. Healing required."
    )
    healing_successfull_msg = (
        "✅ Output fluid volume mesh has been successfully healed to a valid mesh."
    )
    healing_not_successfull_msg = "❌ Output fluid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm."

    if baseline_validation_check(fluid_volume):
        print(validation_successfull_msg)
        return True

    print(validation_not_successfull_msg)

    baseline_heal(fluid_volume)
    if baseline_validation_check(fluid_volume):
        print(healing_successfull_msg)
        return True

    print(healing_not_successfull_msg)
    return None
