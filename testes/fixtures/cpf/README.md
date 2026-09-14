# Cadastro

O formulario web envia o CPF **mascarado**, no formato `000.000.000-00`,
porque a mascara e aplicada no input antes do submit.

O endpoint `POST /api/users` deve devolver `201` quando o cadastro e aceito.
