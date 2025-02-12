ARG BASE_IMAGE=amit-Dell-G15.local:5000/ros2-pytorch:humble-torch2.3.0
FROM $BASE_IMAGE AS base

ARG ROS_DISTRO=humble
ENV ROS_DISTRO=$ROS_DISTRO

RUN DEBIAN_FRONTEND=noninteractive 

RUN echo ${DEBIAN_FRONTEND}
RUN sudo apt-get update && \
    sudo apt-get install -y \
    wget \
    python3-pip \
    python3-argcomplete \
    bash-completion \
    git-lfs \
    i2c-tools \
    libi2c-dev \
    libncurses5-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
RUN sudo apt-get update && \
    sudo apt-get install -y \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

    
# Create the user
# ===================
ARG USERNAME
ENV USERNAME=$USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Check if "ubuntu" user exists, delete it if it does, then create the desired user
RUN if getent passwd ubuntu > /dev/null 2>&1; then \
        userdel -r ubuntu && \
        echo "Deleted existing ubuntu user"; \
    fi && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "Created new user $USERNAME"

# Add sudo support for the non-root user
RUN apt-get update && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*

# Set up autocompletion for user
RUN apt-get update && apt-get install -y git-core bash-completion \
  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc \
  && echo "if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash; fi" >> /home/$USERNAME/.bashrc \
  && rm -rf /var/lib/apt/lists/*

#### SOURSE ROS2 ###
RUN echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc

##### CYCLON DDS #####
RUN echo export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp >> /home/$USERNAME/.bashrc && \
    export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp 

# colcon argcomplete
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /home/$USERNAME/.bashrc
RUN echo "if [ -f /usr/share/bash-completion/completions/git ]; then source /usr/share/bash-completion/completions/git; fi" >> /home/$USERNAME/.bashrc
   
USER $USERNAME

# ======================================
FROM base AS dev

# Install ROS2 development tools:
RUN sudo apt-get update && \
    sudo apt-get install -y \
    ros-dev-tools \
    python3-sphinx \
    && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install \
    sphinx-rtd-theme \
    myst-parser

    

