ARG BASE_IMAGE
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
    i2c-tools \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
RUN pip3 install -U \
    sphinx

RUN sudo apt-get update && \
    sudo apt-get install -y \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-dev-tools \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

    
# Create the user
# ===================
ARG USERNAME
ENV USERNAME=$USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if getent passwd ubuntu > /dev/null 2>&1; then \
        userdel -r ubuntu && \
        echo "Deleted existing ubuntu user"; \
    fi && \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
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
# CMD ["/bin/bash"]


