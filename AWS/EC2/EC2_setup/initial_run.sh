container_name=$1
aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 161266116677.dkr.ecr.us-east-1.amazonaws.com
sudo docker pull 161266116677.dkr.ecr.us-east-1.amazonaws.com/ayata_dev_container:start_script-1
sudo docker run -d -it --network host --user ayata_users -v ~/data/raw:/home/ayata_users/Ayata/pacesetter/pacesetter/data/raw -v ~/data/processed:/home/ayata_users/Ayata/pacesetter/pacesetter/data/processed -v ~/data/interim:/home/ayata_users/Ayata/pacesetter/pacesetter/data/interim -v ~/data/external:/home/ayata_users/Ayata/pacesetter/pacesetter/data/external --name $container_name 161266116677.dkr.ecr.us-east-1.amazonaws.com/ayata_dev_container:start_script-1 bash
echo "The container $container_name is up and running, also ready to use. Run the below commands to go inside the container:"
printf "\n"
echo "sudo docker attach $container_name"
printf "\n"
echo "To initiate a notebook inside container without entering the container run the below command from your terminal"
printf "\n"
echo "sudo docker exec $container_name bash -c 'bash start.sh'"
printf "\n"
