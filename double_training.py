import shutil

from alpha_zero_trainer import execute_command_synch

if __name__ == '__main__':
    execute_command_synch('python alpha_zero_trainer.py --agent "sub_watten_agent_train_default" '
                          '--agent_path "games/sub_watten/training/best.h5" '
                          '--memory_path "games/sub_watten/training/memory.pkl" '
                          '--workspace "games/sub_watten/training" --max_steps 400 --games_num 100 --iterations 100 '
                          '--exploration_decay_steps 15 --skip_evaluation')

    # copia best.h5 in doublegen1.h5
    shutil.copy('games/sub_watten/training/best.h5', 'games/sub_watten/training/doubletrain1.h5')

    execute_command_synch('python alpha_zero_trainer.py --agent "sub_watten_agent_train_default" '
                          '--agent_path "games/sub_watten/training/best.h5" '
                          '--memory_path "games/sub_watten/training/memory.pkl" '
                          '--workspace "games/sub_watten/training" --max_steps 400 --games_num 100 '
                          '--iterations 100 --exploration_decay_steps 15 --skip_evaluation')
