#!/bin/bash

echo "PostgreSQL init started"
export PGPASSWORD=$POSTGRES_PASSWORD

# Check if database exists
if psql -U "$PG_USER" -h "$PG_HOST" -p "$PG_PORT" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Database $DB_NAME already exists"
else
    echo "Creating database $DB_NAME"
    psql -U "$PG_USER" -h "$PG_HOST" -p "$PG_PORT" -c "CREATE DATABASE $DB_NAME"
    
    # Verify creation
    if [ $? -eq 0 ]; then
        echo "Database $DB_NAME created successfully"
    else
        echo "Failed to create database $DB_NAME" >&2
        exit 1
    fi
fi

psql -v ON_ERROR_STOP=1 -h db --port 5432 --username "postgres" -d "auth_db"  <<-EOSQL
         CREATE TABLE IF NOT EXISTS public.users (
            id serial PRIMARY KEY,
            email varchar(100) NOT NULL,
            hashed_password varchar(1000)
         );

         CREATE TABLE IF NOT EXISTS public.refresh_tokens (
            id serial PRIMARY KEY,
            user_id serial REFERENCES users (id),
            token varchar(1000)
         );
EOSQL

# Generate Fake Data :)

# Функция генерации случайного email
generate_email() {
    local domains=("gmail.com" "yahoo.com" "outlook.com" "example.com" "mail.ru" "yandex.ru")
    local chars="abcdefghijklmnopqrstuvwxyz0123456789"
    local username_length=$(( RANDOM % 10 + 5 ))  # Длина имени от 5 до 14 символов
    local username=""

    # Генерируем случайное имя пользователя
    for (( i=0; i<$username_length; i++ )); do
        username+=${chars:$(( RANDOM % ${#chars} )):1}
    done

    # Выбираем случайный домен
    local domain=${domains[$RANDOM % ${#domains[@]}]}

    echo "${username}@${domain}"
}

generate_password() {
   DEFAULT_LENGTH=16
   length=${1:-$DEFAULT_LENGTH}
   algorithm=${2:-sha256}

   # Generate random password (alphanumeric + special chars)
   password=$(tr -dc 'A-Za-z0-9!@#$%^&*()_+-=' < /dev/urandom | head -c "$length")

   # Output results
   echo "$password"
}

generate_hash() {
   # Generate hash
   case $algorithm in
      md5)
         hash=$(echo -n "$password" | md5sum | awk '{print $1}')
         ;;
      sha1)
         hash=$(echo -n "$password" | sha1sum | awk '{print $1}')
         ;;
      sha256)
         hash=$(echo -n "$password" | sha256sum | awk '{print $1}')
         ;;
      sha512)
         hash=$(echo -n "$password" | sha512sum | awk '{print $1}')
         ;;
      bcrypt)
         if ! command -v htpasswd &> /dev/null; then
               echo "Error: htpasswd not found. Install apache2-utils for bcrypt support."
               exit 1
         fi
         hash=$(echo -n "$password" | htpasswd -nbiB "" | cut -d: -f2)
         ;;
      *)
         echo "Unsupported algorithm: $algorithm"
         echo "Available options: md5, sha1, sha256, sha512, bcrypt"
         exit 1
         ;;
   esac
   echo "$hash"
}

count=10
echo "" > fake_data.sql
for (( i=0; i<$count; i++ )); do
   email=$(generate_email)
   password=$(generate_password)

   echo "INSERT INTO public.users (email, hashed_password) VALUES('$email', '$password');" >> fake_data.sql
done

cat fake_data.sql
psql -h db --port 5432 -U postgres -d auth_db -f fake_data.sql

echo "PostgreSQL init ended"

touch /tmp/ready && exit 0