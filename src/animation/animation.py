import random
import sys
import time

import colors

LOADING_ANIMATION = ["......", "{c}*{r}.....", ".{c}*{r}....", "..{c}*{r}...", "...{c}*{r}..", "....{c}*{r}.",
                     ".....{c}*{r}",
                     "....{c}*{r}.", "...{c}*{r}..", "..{c}*{r}...", ".{c}*{r}....", "{c}*{r}.....", "......"]
ANIMATION_ITERATION = 0.3


def animate_loading():
    """
    Animates loading.
    """
    for i in range(len(LOADING_ANIMATION)):
        time.sleep(ANIMATION_ITERATION)
        sys.stdout.write("\rScanning for devices. " + LOADING_ANIMATION[i % len(LOADING_ANIMATION)].format(
            c=random.choice(colors.all_colors), r=colors.RESET
        ))
        sys.stdout.flush()