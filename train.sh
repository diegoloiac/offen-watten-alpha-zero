python3 alpha_zero_trainer.py \
--agent "hand_watten_train" \
--workspace "versions/hand_watten/training/ffnn/raise" \
--agent_path "versions/hand_watten/training/ffnn/raise/best.h5" \
--max_steps 400 \
--games_num 100 \
--iterations 600 \
--exploration_decay_steps 15 \
--epochs 1
