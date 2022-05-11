#pragma once

#include <vector>
#include <Eigen/Core>
#include <limits>
#include <queue>
#include "sofm/types.h"

namespace sofm
{
    namespace art
    {
        class OnlineFuzzyART
        {
        private:
            double rho_;
            double alpha_;
            double beta_;
            int num_features_;
            int num_clusters_;
            int iterations_ = 0;
            Matrix w_;

            int eval_pattern(const VectorConstRef pattern);
            int train_pattern(const VectorConstRef pattern);

        public:
            OnlineFuzzyART(double rho, double alpha, double beta, int num_features);
            std::vector<int> run_online(const MatrixConstRef features, int max_epochs = std::numeric_limits<int>::max());
        };

        struct Activation
        {
            Activation(double a, size_t i) : activation(a), index(i) {}
            bool operator<(const Activation &rhs) const
            {
                return activation < rhs.activation;
            }
            bool operator>(const Activation &rhs) const
            {
                return activation > rhs.activation;
            }
            bool operator==(const Activation &rhs) const
            {
                return (activation == rhs.activation) && (index == rhs.index);
            }
            bool operator>=(const Activation &rhs) const
            {
                return ((*this) > rhs) || ((*this) == rhs);
            }
            bool operator<=(const Activation &rhs) const
            {
                return ((*this) < rhs) || ((*this) == rhs);
            }

            double activation;
            size_t index;
        };

        using ActivationQueue =
            std::priority_queue<Activation>;

    } // namespace art

} // namespace sofm
