import shutil

from alpha_zero_trainer import execute_command_synch

if __name__ == '__main__':
    execute_command_synch('python alpha_zero_trainer.py --agent "asymmetric_sub_watten_agent_train_default"'
                          '--agent_path "games/asymmetric_sub_watten/training/v2/best.h5" '
                          '--memory_path "games/asymmetric_sub_watten/training/v2/memory.pkl" '
                          '--workspace "games/asymmetric_sub_watten/training/v2" --max_steps 400 '
                          '--games_num 100 --iterations 100 '
                          '--exploration_decay_steps 15 --skip_evaluation')

    # copia best.h5 in doublegen1.h5
    shutil.copy('games/asymmetric_sub_watten/training/v2/best.h5',
                'games/asymmetric_sub_watten/training/v2/doubletrain1.h5')

    execute_command_synch('python alpha_zero_trainer.py --agent "asymmetric_sub_watten_agent_train_default" '
                          '--agent_path "games/asymmetric_sub_watten/training/v2/best.h5" '
                          '--memory_path "games/asymmetric_sub_watten/training/v2/memory.pkl" '
                          '--workspace "games/asymmetric_sub_watten/training/v2" --max_steps 400 --games_num 100 '
                          '--iterations 100 --exploration_decay_steps 15 --skip_evaluation')
