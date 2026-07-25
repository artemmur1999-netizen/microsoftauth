from microsoftauth import MicrosoftAuth

# Инициализация авторизации Microsoft с 4 параметрами
MicrosoftAuth("Your Client ID", ["User.Read"], "all", None)

# 1st Client ID: Obtain it via the "register application" function.
# 2nd Scopes: Permissions list, e.g., ["User.Read"]. Pass None for default.
# 3rd Account type: "all" supports both personal and work/education accounts.
# 4th Custom account type: Pass a specific tenant ID string here, or None for default.
